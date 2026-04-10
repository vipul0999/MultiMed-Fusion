import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc26", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(26, { page, browser, request, context, baseURL });
});
