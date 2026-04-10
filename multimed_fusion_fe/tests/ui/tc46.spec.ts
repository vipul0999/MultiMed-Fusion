import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc46", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(46, { page, browser, request, context, baseURL });
});
