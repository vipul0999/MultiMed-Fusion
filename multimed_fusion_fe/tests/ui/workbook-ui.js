import { expect } from "@playwright/test";

import {
  UI_BASE_URL,
  apiLogin,
  apiRegister,
  authorizedRequest,
  approveThroughUi,
  bootSession,
  closeUploadRequest,
  doctorRequestUpload,
  fileFromPath,
  inlineFile,
  mockAnalyzeFailure,
  mockAnalyzeSuccess,
  mockChatResponse,
  mockPatientSearch,
  patientUpload,
  pauseIfRequested,
  realFiles,
  revokeAccess,
  seedApprovedDoctorAndPatient,
  seedDoctorAndPatient,
  selectApprovedDoctor,
  selectApprovedPatient,
  sendQuestion,
  analyzeFirstVisibleFile,
  uiLogin,
  uniqueUser,
} from "./helpers";

async function uploadDocuments(page, doctorUsername) {
  await patientUpload(page, doctorUsername, [
    fileFromPath(realFiles.pdf, "application/pdf"),
    inlineFile("lab_report.txt", "text/plain", "Diagnosis: Stable\nMedication: Aspirin"),
  ]);
}

async function uploadImages(page, doctorUsername) {
  await patientUpload(page, doctorUsername, [
    fileFromPath(realFiles.image, "image/png"),
    inlineFile("scan.jpg", "image/jpeg", "mock jpg image"),
    inlineFile("ct_scan.dcm", "application/dicom", "mock dicom content"),
  ]);
}

async function uploadAudio(page, doctorUsername) {
  await patientUpload(page, doctorUsername, [
    fileFromPath(realFiles.audio, "audio/mpeg"),
    inlineFile("patient_voice.wav", "audio/wav", "mock wav audio"),
  ]);
}

async function setupApprovedFlow({ browser, request }) {
  const { doctor, patient } = await seedApprovedDoctorAndPatient(request);
  const patientContext = await browser.newContext();
  const doctorContext = await browser.newContext();
  const patientPage = await patientContext.newPage();
  const doctorPage = await doctorContext.newPage();
  await bootSession(patientPage, request, patient);
  await bootSession(doctorPage, request, doctor);
  return { doctor, patient, patientPage, doctorPage, patientContext, doctorContext };
}

async function setupSinglePatientFlow({ page, request }) {
  const { doctor, patient } = await seedApprovedDoctorAndPatient(request);
  await bootSession(page, request, patient);
  return { doctor, patient, page };
}

async function setupSingleDoctorFlow({ page, request }) {
  const { doctor, patient } = await seedApprovedDoctorAndPatient(request);
  await bootSession(page, request, doctor);
  return { doctor, patient, page };
}

async function finish({ page, extraPages = [] }) {
  await pauseIfRequested(page);
  for (const target of extraPages) {
    if (target && typeof target.close === "function") {
      try {
        await target.close();
      } catch {}
    }
  }
}

export async function runWorkbookUiCase(tc, ctx) {
  switch (tc) {
    case 1: {
      const flow = await setupSinglePatientFlow(ctx);
      await uploadDocuments(flow.page, flow.doctor.username);
      await finish({ page: flow.page, extraPages: [] });
      return;
    }
    case 2: {
      const flow = await setupSinglePatientFlow(ctx);
      await uploadImages(flow.page, flow.doctor.username);
      await finish({ page: flow.page, extraPages: [] });
      return;
    }
    case 3: {
      const flow = await setupSinglePatientFlow(ctx);
      await uploadAudio(flow.page, flow.doctor.username);
      await finish({ page: flow.page, extraPages: [] });
      return;
    }
    case 4:
    case 5:
    case 6:
    case 7:
    case 8:
    case 22:
    case 23:
    case 24: {
      const flow = await setupApprovedFlow(ctx);
      if ([4, 22].includes(tc)) await uploadDocuments(flow.patientPage, flow.doctor.username);
      if ([5].includes(tc)) await patientUpload(flow.patientPage, flow.doctor.username, [inlineFile("discharge_summary.txt", "text/plain", "Diagnosis: Flu")]);
      if ([6, 23].includes(tc)) await patientUpload(flow.patientPage, flow.doctor.username, [fileFromPath(realFiles.image, "image/png")]);
      if ([7, 24].includes(tc)) await patientUpload(flow.patientPage, flow.doctor.username, [fileFromPath(realFiles.audio, "audio/mpeg")]);
      if ([8].includes(tc)) await patientUpload(flow.patientPage, flow.doctor.username, [inlineFile("patient_followup.wav", "audio/wav", "mock wav")]);
      await mockAnalyzeSuccess(flow.doctorPage, flow.patient, flow.doctor);
      await selectApprovedPatient(flow.doctorPage, flow.patient.username);
      const response = await analyzeFirstVisibleFile(flow.doctorPage);
      expect(response.ok()).toBeTruthy();
      await finish({ page: flow.doctorPage, extraPages: [flow.patientPage, flow.patientContext, flow.doctorContext] });
      return;
    }
    case 9: {
      const flow = await setupApprovedFlow(ctx);
      await patientUpload(flow.patientPage, flow.doctor.username, [fileFromPath(realFiles.audio, "audio/mpeg")]);
      await mockAnalyzeFailure(flow.doctorPage, "Transcription failed.");
      await selectApprovedPatient(flow.doctorPage, flow.patient.username);
      const response = await analyzeFirstVisibleFile(flow.doctorPage);
      expect(response.ok()).toBeFalsy();
      await finish({ page: flow.doctorPage, extraPages: [flow.patientPage, flow.patientContext, flow.doctorContext] });
      return;
    }
    case 10:
    case 11:
    case 12:
    case 16:
    case 17:
    case 18:
    case 19:
    case 20:
    case 21:
    case 25:
    case 26:
    case 27: {
      const flow = await setupApprovedFlow(ctx);
      await uploadDocuments(flow.patientPage, flow.doctor.username);
      await selectApprovedPatient(flow.doctorPage, flow.patient.username);
      const sources =
        tc === 25
          ? [{ file_id: "file-1", name: "pdf_file2.pdf", hyperlink: UI_BASE_URL, download_url: UI_BASE_URL, uploaded_by_role: "patient" }]
          : tc === 26 || tc === 27
            ? [
                { file_id: "file-1", name: "pdf_file2.pdf", hyperlink: UI_BASE_URL, download_url: UI_BASE_URL, uploaded_by_role: "patient" },
                { file_id: "file-2", name: "lab_report.txt", hyperlink: UI_BASE_URL, download_url: UI_BASE_URL, uploaded_by_role: "patient" },
              ]
            : [];
      await mockChatResponse(flow.doctorPage, `Scenario tc${tc} answer`, {
        patientId: flow.patient.id,
        doctorId: flow.doctor.id,
        sources,
        selectedFileIds: sources.map((s) => s.file_id),
      });
      const response = await sendQuestion(flow.doctorPage, `Run tc${tc} question`);
      if (tc === 11) {
        expect(response.ok()).toBeTruthy();
      } else {
        expect(response.ok()).toBeTruthy();
      }
      await expect(flow.doctorPage.getByText(`Scenario tc${tc} answer`)).toBeVisible();
      if (sources.length) {
        await expect(flow.doctorPage.locator(".source-chip")).toHaveCount(sources.length);
      }
      await finish({ page: flow.doctorPage, extraPages: [flow.patientPage, flow.patientContext, flow.doctorContext] });
      return;
    }
    case 13:
    case 14: {
      const flow = await setupApprovedFlow(ctx);
      await uploadDocuments(flow.patientPage, flow.doctor.username);
      await selectApprovedPatient(flow.doctorPage, flow.patient.username);
      await mockChatResponse(flow.doctorPage, tc === 13 ? "English query accepted." : "Medical abbreviations processed.");
      await sendQuestion(flow.doctorPage, tc === 13 ? "What is the diagnosis?" : "Summarize HTN and BP guidance");
      await expect(flow.doctorPage.getByText(tc === 13 ? "English query accepted." : "Medical abbreviations processed.")).toBeVisible();
      await finish({ page: flow.doctorPage, extraPages: [flow.patientPage, flow.patientContext, flow.doctorContext] });
      return;
    }
    case 15: {
      const flow = await setupApprovedFlow(ctx);
      await uploadDocuments(flow.patientPage, flow.doctor.username);
      await selectApprovedPatient(flow.doctorPage, flow.patient.username);
      await mockChatResponse(flow.doctorPage, "Only English natural language queries are supported.", { status: 400 });
      const response = await sendQuestion(flow.doctorPage, "¿Cuál es el diagnóstico?");
      expect(response.ok()).toBeFalsy();
      await finish({ page: flow.doctorPage, extraPages: [flow.patientPage, flow.patientContext, flow.doctorContext] });
      return;
    }
    case 28:
    case 29:
    case 30:
    case 34:
    case 35:
    case 36: {
      const flow = await setupApprovedFlow(ctx);
      await patientUpload(flow.patientPage, flow.doctor.username, [
        inlineFile("patient11_01-01-1990_report.pdf", "application/pdf", "mock sensitive pdf"),
      ]);
      await selectApprovedDoctor(flow.patientPage, flow.doctor.username);
      await expect(flow.patientPage.locator("body")).not.toContainText("patient11");
      await expect(flow.patientPage.locator("body")).not.toContainText("01-01-1990");
      await finish({ page: flow.patientPage, extraPages: [flow.doctorPage, flow.patientContext, flow.doctorContext] });
      return;
    }
    case 31: {
      const flow = await setupSingleDoctorFlow(ctx);
      await selectApprovedPatient(flow.page, flow.patient.username);
      await expect(flow.page.getByText(flow.patient.username)).toBeVisible();
      await finish({ page: flow.page, extraPages: [] });
      return;
    }
    case 32:
    case 33: {
      const { doctor, patient } = await seedDoctorAndPatient(ctx.request);
      const otherDoctor = await apiRegister(ctx.request, uniqueUser("doctoruiother", "doctor"));
      const doctorContext = await ctx.browser.newContext();
      const page = await doctorContext.newPage();
      await bootSession(page, ctx.request, otherDoctor);
      await expect(page.getByTestId(`doctor-approved-patient-${patient.username}`)).toHaveCount(0);
      await finish({ page, extraPages: [doctorContext] });
      return;
    }
    case 37:
    case 39: {
      const flow = await setupApprovedFlow(ctx);
      await revokeAccess(flow.patientPage, flow.doctor.username);
      await finish({ page: flow.patientPage, extraPages: [flow.doctorPage, flow.patientContext, flow.doctorContext] });
      return;
    }
    case 38: {
      const flow = await setupSinglePatientFlow(ctx);
      await expect(flow.page.getByTestId(`patient-approved-doctor-${flow.doctor.username}`)).toBeVisible();
      await finish({ page: flow.page, extraPages: [] });
      return;
    }
    case 40: {
      const page = await ctx.browser.newPage();
      const user = uniqueUser("registerui", "patient");
      await page.goto("/register");
      await page.getByLabel("Username").fill(user.username);
      await page.getByLabel("Email").fill(user.email);
      await page.getByLabel("Password").fill(user.password);
      await page.getByLabel("Role").selectOption("patient");
      await page.getByRole("button", { name: "Create account" }).click();
      await expect(page.getByText("Account created. Please sign in.")).toBeVisible();
      await finish({ page, extraPages: [] });
      return;
    }
    case 41: {
      const user = await apiRegister(ctx.request, uniqueUser("passwordui", "patient"));
      await authorizedRequest(ctx.request, user, "POST", "/api/auth/password/update/", {
        old_password: user.password,
        new_password: "NewPassword@123",
      });
      const page = await ctx.browser.newPage();
      await uiLogin(page, user.username, "NewPassword@123");
      await expect(page.getByTestId("patient-workspace")).toBeVisible();
      await finish({ page, extraPages: [] });
      return;
    }
    case 42: {
      const user = await apiRegister(ctx.request, uniqueUser("loginapiui", "doctor"));
      const session = await apiLogin(ctx.request, user);
      expect(JSON.stringify(session)).not.toContain(user.password);
      const page = await ctx.browser.newPage();
      await uiLogin(page, user.username, user.password);
      await expect(page.getByTestId("doctor-workspace")).toBeVisible();
      await finish({ page, extraPages: [] });
      return;
    }
    case 43:
    case 45: {
      const flow = await setupSinglePatientFlow(ctx);
      await patientUpload(flow.page, flow.doctor.username, [fileFromPath(realFiles.pdf, "application/pdf")]);
      if (tc === 45) {
        await patientUpload(flow.page, flow.doctor.username, [fileFromPath(realFiles.image, "image/png")]);
      }
      await finish({ page: flow.page, extraPages: [] });
      return;
    }
    case 44: {
      const flow = await setupApprovedFlow(ctx);
      await uploadDocuments(flow.patientPage, flow.doctor.username);
      await selectApprovedPatient(flow.doctorPage, flow.patient.username);
      const fileRow = flow.doctorPage.locator('[data-testid^="doctor-file-row-"]').first();
      await expect(fileRow).toBeVisible();
      await finish({ page: flow.doctorPage, extraPages: [flow.patientPage, flow.patientContext, flow.doctorContext] });
      return;
    }
    case 46:
    case 47:
    case 48: {
      const flow = await setupApprovedFlow(ctx);
      const files =
        tc === 46
          ? [fileFromPath(realFiles.docx, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"), fileFromPath(realFiles.audio, "audio/mpeg")]
          : tc === 47
            ? [fileFromPath(realFiles.image, "image/png"), fileFromPath(realFiles.docx, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")]
            : [
                fileFromPath(realFiles.docx, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
                fileFromPath(realFiles.audio, "audio/mpeg"),
                fileFromPath(realFiles.image, "image/png"),
              ];
      await patientUpload(flow.patientPage, flow.doctor.username, files);
      await mockAnalyzeSuccess(flow.doctorPage, flow.patient, flow.doctor);
      await selectApprovedPatient(flow.doctorPage, flow.patient.username);
      const response = await analyzeFirstVisibleFile(flow.doctorPage);
      expect(response.ok()).toBeTruthy();
      await finish({ page: flow.doctorPage, extraPages: [flow.patientPage, flow.patientContext, flow.doctorContext] });
      return;
    }
    default:
      throw new Error(`Unsupported UI workbook case tc${tc}`);
  }
}
