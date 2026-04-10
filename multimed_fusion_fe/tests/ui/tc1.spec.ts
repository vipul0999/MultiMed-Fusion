import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc1", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(1, { page, browser, request, context, baseURL });
});
