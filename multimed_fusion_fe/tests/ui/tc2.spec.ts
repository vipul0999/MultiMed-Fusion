import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc2", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(2, { page, browser, request, context, baseURL });
});
