import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc4", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(4, { page, browser, request, context, baseURL });
});
