import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc30", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(30, { page, browser, request, context, baseURL });
});
