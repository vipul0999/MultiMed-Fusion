import path from "node:path";
import fs from "node:fs";
import { expect } from "@playwright/test";

export const UI_BASE_URL = process.env.UI_BASE_URL || "http://127.0.0.1:5173";
export const API_BASE_URL = process.env.UI_BACKEND_BASE_URL || "http://127.0.0.1:8000";
const AUTH_STORAGE_KEY = "ehr_portal_auth";
const TEST_DATA_DIR = process.env.GDP_UI_TEST_DATA_DIR || "/mnt/c/Users/s576701/Documents/gdp files";

export const realFiles = {
  pdf: path.join(TEST_DATA_DIR, "pdf_file2.pdf"),
  docx: path.join(TEST_DATA_DIR, "document4.docx"),
  image: path.join(TEST_DATA_DIR, "images2.png"),
  audio: path.join(TEST_DATA_DIR, "audios4.mp3"),
};

export const seededUsers = {
  doctor: { username: process.env.UI_DOCTOR_USERNAME || "doctor11", password: process.env.UI_PASSWORD || "password", role: "doctor" },
  patient: { username: process.env.UI_PATIENT_USERNAME || "patient11", password: process.env.UI_PASSWORD || "password", role: "patient" },
};

export function uniqueUser(prefix, role) {
  const stamp = `${Date.now()}${Math.floor(Math.random() * 100000)}`;
  return {
    username: `${prefix}${stamp}`,
    email: `${prefix}${stamp}@example.com`,
    password: "Password@123",
    role,
  };
}

export async function pauseIfRequested(page) {
  if (process.env.PW_STAY_OPEN === "1") {
    await page.pause();
  }
}

export async function apiRegister(request, user) {
  const response = await request.post(`${API_BASE_URL}/api/auth/register/`, {
    data: {
      username: user.username,
      email: user.email,
      password: user.password,
      role: user.role,
    },
  });
  expect(response.ok()).toBeTruthy();
  const payload = await response.json();
  return { ...user, ...payload };
}

export async function apiLogin(request, user) {
  const response = await request.post(`${API_BASE_URL}/api/auth/login/`, {
    data: { username: user.username, password: user.password },
  });
  expect(response.ok()).toBeTruthy();
  return await response.json();
}

export async function authorizedRequest(request, user, method, url, data) {
  const session = await apiLogin(request, user);
  const response = await request.fetch(`${API_BASE_URL}${url}`, {
    method,
    headers: {
      Authorization: `Bearer ${session.access}`,
      "Content-Type": "application/json",
    },
    data: data ? JSON.stringify(data) : undefined,
  });
  expect(response.ok()).toBeTruthy();
  return response;
}

export async function apiGrantAccess(request, patient, doctor) {
  await authorizedRequest(request, patient, "POST", "/api/portal/patient/grant-doctor/", {
    doctor_id: doctor.id,
    note: "Approved for UI testing",
  });
}

export async function apiRequestAccess(request, doctor, patient) {
  await authorizedRequest(request, doctor, "POST", "/api/portal/doctor/request-access/", {
    patient_id: patient.id,
    note: "Requesting chart access.",
  });
}

export async function apiCreateUploadRequest(request, doctor, patient, message = "Please upload records for review.") {
  await authorizedRequest(request, doctor, "POST", "/api/portal/doctor/upload-request/", {
    patient_id: patient.id,
    message,
  });
}

export async function seedDoctorAndPatient(request) {
  const doctor = await apiRegister(request, uniqueUser("doctorui", "doctor"));
  const patient = await apiRegister(request, uniqueUser("patientui", "patient"));
  return { doctor, patient };
}

export async function seedApprovedDoctorAndPatient(request) {
  const pair = await seedDoctorAndPatient(request);
  await apiGrantAccess(request, pair.patient, pair.doctor);
  return pair;
}

export async function bootSession(page, request, user) {
  const session = await apiLogin(request, user);
  await page.addInitScript(
    ([storageKey, payload]) => {
      window.sessionStorage.setItem(storageKey, JSON.stringify(payload));
    },
    [AUTH_STORAGE_KEY, { access: session.access, refresh: session.refresh, user: session.user }],
  );
  await page.goto(user.role === "doctor" ? "/app/doctor" : user.role === "patient" ? "/app/patient" : "/login");
  await expect(page.getByTestId(`${user.role}-workspace`)).toBeVisible();
}

export async function uiLogin(page, username, password) {
  await page.goto("/login");
  await page.getByTestId("login-username").fill(username);
  await page.getByTestId("login-password").fill(password);
  await page.getByTestId("login-submit").click();
}

export async function logout(page, role) {
  await page.getByTestId(`${role}-signout`).click();
  await expect(page.getByTestId("login-submit")).toBeVisible();
}

export function mockPatientSearch(page, patient) {
  return page.route("**/api/portal/doctor/patient-search/**", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify([
        { id: patient.id, username: patient.username, email: patient.email },
      ]),
    });
  });
}

export function mockAnalyzeSuccess(page, patient, doctor) {
  return page.route("**/api/medfiles/doctor/analyze/", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        message: "Files analyzed successfully.",
        patient_id: patient.id,
        doctor_id: doctor.id,
        batch_hash: "mock-batch",
        chunks_created: 1,
        embedding_model: "mock-model",
        errors: [],
        files: [],
      }),
    });
  });
}

export function mockAnalyzeFailure(page, detail = "Unable to analyze files.") {
  return page.route("**/api/medfiles/doctor/analyze/", async (route) => {
    await route.fulfill({
      status: 400,
      contentType: "application/json",
      body: JSON.stringify({ detail }),
    });
  });
}

export function mockChatResponse(page, answer, options = {}) {
  return page.route("**/api/medfiles/doctor/chat-query/", async (route) => {
    await route.fulfill({
      status: options.status || 200,
      contentType: "application/json",
      body: JSON.stringify(
        options.status && options.status >= 400
          ? { detail: answer }
          : {
              message: "Query processed successfully.",
              patient_id: options.patientId || "mock-patient",
              doctor_id: options.doctorId || "mock-doctor",
              query: options.query || "What is the summary?",
              chunks_retrieved: 1,
              chunks: options.chunks || [],
              context: options.context || "",
              summary: answer,
              confidence: options.confidence || "high",
              gemini_ok: true,
              retrieval_mode: options.retrievalMode || "selected_file_full_context",
              sources: options.sources || [],
              selected_file_ids: options.selectedFileIds || [],
            },
      ),
    });
  });
}

export function inlineFile(name, mimeType, content) {
  return { name, mimeType, buffer: Buffer.from(content) };
}

export function fileFromPath(filePath, mimeType) {
  return {
    name: path.basename(filePath),
    mimeType,
    buffer: fs.readFileSync(filePath),
  };
}

export async function requestAccessThroughUi(page, patientUsername) {
  await page.getByTestId("doctor-search-patient").fill(patientUsername);
  await page.waitForResponse((response) => response.url().includes("/api/portal/doctor/patient-search/"));
  const row = page.getByTestId(`doctor-search-result-${patientUsername}`);
  await expect(row).toBeVisible();
  const responsePromise = page.waitForResponse(
    (response) => response.url().includes("/api/portal/doctor/request-access/") && response.request().method() === "POST",
  );
  await page.getByTestId(`doctor-request-access-${patientUsername}`).click({ force: true });
  const response = await responsePromise;
  expect(response.ok()).toBeTruthy();
}

export async function approveThroughUi(page, doctorUsername) {
  const row = page.getByTestId(`patient-pending-request-${doctorUsername}`);
  await expect(row).toBeVisible();
  const responsePromise = page.waitForResponse(
    (response) => response.url().includes("/decision/") && response.request().method() === "POST",
  );
  await page.getByTestId(`patient-approve-request-${doctorUsername}`).click({ force: true });
  const response = await responsePromise;
  expect(response.ok()).toBeTruthy();
}

export async function rejectThroughUi(page, doctorUsername) {
  const row = page.getByTestId(`patient-pending-request-${doctorUsername}`);
  await expect(row).toBeVisible();
  const responsePromise = page.waitForResponse(
    (response) => response.url().includes("/decision/") && response.request().method() === "POST",
  );
  await page.getByTestId(`patient-reject-request-${doctorUsername}`).click({ force: true });
  const response = await responsePromise;
  expect(response.ok()).toBeTruthy();
}

export async function selectApprovedDoctor(page, doctorUsername) {
  await page.getByTestId("patient-refresh").click();
  await expect(page.getByTestId(`patient-approved-doctor-${doctorUsername}`)).toBeVisible();
  await page.getByTestId(`patient-approved-doctor-${doctorUsername}`).click({ force: true });
}

export async function selectApprovedPatient(page, patientUsername) {
  await page.getByTestId("doctor-refresh").click();
  await expect(page.getByTestId(`doctor-approved-patient-${patientUsername}`)).toBeVisible();
  await page.getByTestId(`doctor-approved-patient-${patientUsername}`).click({ force: true });
}

export async function patientUpload(page, doctorUsername, files) {
  await selectApprovedDoctor(page, doctorUsername);
  const responsePromise = page.waitForResponse(
    (response) => response.url().includes("/api/medfiles/patient/upload/") && response.request().method() === "POST",
  );
  await page.getByTestId("patient-upload-files-input").setInputFiles(files);
  await page.getByTestId("patient-upload-submit").click();
  const response = await responsePromise;
  expect(response.ok()).toBeTruthy();
}

export async function doctorRequestUpload(page, message) {
  const responsePromise = page.waitForResponse(
    (response) => response.url().includes("/api/portal/doctor/upload-request/") && response.request().method() === "POST",
  );
  await page.getByTestId("doctor-upload-request-message").fill(message);
  await page.getByTestId("doctor-upload-request-submit").click();
  const response = await responsePromise;
  expect(response.ok()).toBeTruthy();
}

export async function closeUploadRequest(page, doctorUsername) {
  await expect(page.getByTestId(`patient-upload-request-${doctorUsername}`)).toBeVisible();
  const responsePromise = page.waitForResponse(
    (response) => response.url().includes("/close/") && response.request().method() === "POST",
  );
  await page.getByTestId(`patient-close-upload-request-${doctorUsername}`).click({ force: true });
  const response = await responsePromise;
  expect(response.ok()).toBeTruthy();
}

export async function analyzeFirstVisibleFile(page) {
  const checkbox = page.locator('[data-testid^="doctor-file-checkbox-"]').first();
  await expect(checkbox).toBeVisible();
  await checkbox.check({ force: true });
  const responsePromise = page.waitForResponse((response) => response.url().includes("/api/medfiles/doctor/analyze/"));
  await page.getByTestId("doctor-analyze-selected").click();
  return await responsePromise;
}

export async function sendQuestion(page, question) {
  const responsePromise = page.waitForResponse((response) => response.url().includes("/api/medfiles/doctor/chat-query/"));
  await page.getByTestId("doctor-chat-question").fill(question);
  await page.getByTestId("doctor-chat-send").click();
  return await responsePromise;
}

export async function revokeAccess(page, doctorUsername) {
  await selectApprovedDoctor(page, doctorUsername);
  const responsePromise = page.waitForResponse((response) => response.url().includes("/api/portal/access/") && response.request().method() === "POST");
  await page.getByTestId("patient-revoke-access").click({ force: true });
  const response = await responsePromise;
  expect(response.ok()).toBeTruthy();
}
