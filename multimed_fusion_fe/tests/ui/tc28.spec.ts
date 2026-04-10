import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc28", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(28, { page, browser, request, context, baseURL });
});
