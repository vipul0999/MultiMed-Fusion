import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc8", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(8, { page, browser, request, context, baseURL });
});
