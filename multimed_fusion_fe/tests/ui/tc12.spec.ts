import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc12", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(12, { page, browser, request, context, baseURL });
});
