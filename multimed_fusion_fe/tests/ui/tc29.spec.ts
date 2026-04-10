import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc29", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(29, { page, browser, request, context, baseURL });
});
