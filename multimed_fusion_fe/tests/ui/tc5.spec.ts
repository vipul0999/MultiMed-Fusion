import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc5", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(5, { page, browser, request, context, baseURL });
});
