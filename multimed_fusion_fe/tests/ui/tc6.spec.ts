import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc6", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(6, { page, browser, request, context, baseURL });
});
