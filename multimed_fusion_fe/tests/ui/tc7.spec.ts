import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc7", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(7, { page, browser, request, context, baseURL });
});
