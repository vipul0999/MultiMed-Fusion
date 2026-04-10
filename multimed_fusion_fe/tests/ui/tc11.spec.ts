import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc11", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(11, { page, browser, request, context, baseURL });
});
