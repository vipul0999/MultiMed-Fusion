import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc41", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(41, { page, browser, request, context, baseURL });
});
