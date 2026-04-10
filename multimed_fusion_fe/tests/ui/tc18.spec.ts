import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc18", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(18, { page, browser, request, context, baseURL });
});
