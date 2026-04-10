import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc34", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(34, { page, browser, request, context, baseURL });
});
