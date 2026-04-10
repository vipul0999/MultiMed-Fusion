import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc42", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(42, { page, browser, request, context, baseURL });
});
