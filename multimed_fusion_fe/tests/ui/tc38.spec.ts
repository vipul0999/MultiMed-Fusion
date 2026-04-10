import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc38", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(38, { page, browser, request, context, baseURL });
});
