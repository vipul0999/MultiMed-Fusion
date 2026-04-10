import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc43", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(43, { page, browser, request, context, baseURL });
});
