import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc48", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(48, { page, browser, request, context, baseURL });
});
