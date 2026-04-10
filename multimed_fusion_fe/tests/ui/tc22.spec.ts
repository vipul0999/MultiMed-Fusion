import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc22", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(22, { page, browser, request, context, baseURL });
});
