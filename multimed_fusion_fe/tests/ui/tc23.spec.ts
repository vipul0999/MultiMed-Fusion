import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc23", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(23, { page, browser, request, context, baseURL });
});
