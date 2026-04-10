import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc19", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(19, { page, browser, request, context, baseURL });
});
