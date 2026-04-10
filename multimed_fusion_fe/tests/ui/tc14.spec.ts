import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc14", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(14, { page, browser, request, context, baseURL });
});
