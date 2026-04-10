import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc15", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(15, { page, browser, request, context, baseURL });
});
