import test from "node:test";
import assert from "node:assert/strict";
import {
  accessDeniedRedirect,
  isAllowedStudyEmail,
  isPublicAuthPath,
  normalizeEmail,
  safeNextPath,
} from "./study-access.mjs";

test("allows only the exact study account, case-insensitively", () => {
  assert.equal(isAllowedStudyEmail("cvamsik99@gmail.com"), true);
  assert.equal(isAllowedStudyEmail("CVAMSIK99@GMAIL.COM"), true);
  assert.equal(isAllowedStudyEmail("other@example.com"), false);
  assert.equal(isAllowedStudyEmail("cvamsik99@gmail.com.evil.example"), false);
});

test("normalizes whitespace and casing without changing the identity", () => {
  assert.equal(normalizeEmail("  CVamsik99@Gmail.com  "), "cvamsik99@gmail.com");
  assert.equal(normalizeEmail(null), "");
});

test("accepts only local next paths", () => {
  assert.equal(safeNextPath("/00-strategy/INDEX.md"), "/00-strategy/INDEX.md");
  assert.equal(safeNextPath("https://evil.example"), "/");
  assert.equal(safeNextPath("//evil.example"), "/");
  assert.equal(safeNextPath("\\\\evil.example"), "/");
  assert.equal(safeNextPath(""), "/");
});

test("keeps only auth entry points public", () => {
  assert.equal(isPublicAuthPath("/auth/login.html"), true);
  assert.equal(isPublicAuthPath("/auth/callback.html"), true);
  assert.equal(isPublicAuthPath("/auth/session"), true);
  assert.equal(isPublicAuthPath("/favicon.svg"), true);
  assert.equal(isPublicAuthPath("/00-strategy/INDEX.md"), false);
});

test("uses the personal host for a denied study session", () => {
  assert.equal(accessDeniedRedirect(), "https://personal.buildora.work/?study=access-denied");
});
