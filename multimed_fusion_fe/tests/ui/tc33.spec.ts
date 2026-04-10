import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc33", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(33, { page, browser, request, context, baseURL });
});
