/**
 * SDK Constraint Surface: Bookmarks API (Brownfield)
 *
 * Types and interfaces derived from docs/spec-bookmark-manager.md during
 * brownfield onboarding—not copied from legacy Express handlers.
 */

// Domain Types

export interface Bookmark {
  id: string;
  user_id: string;
  url: string;
  title: string;
  description: string;
  tags: string[];
  created_at: Date;
  updated_at: Date;
}

export interface CreateBookmarkInput {
  url: string;
  title?: string;
  description?: string;
  tags?: string[];
}

export interface UpdateBookmarkInput {
  url?: string;
  title?: string;
  description?: string;
  tags?: string[];
}

export interface BookmarkFilter {
  tag?: string;
}

export interface BulkImportItemFailure {
  url: string;
  reason: string;
}

export interface BulkImportResult {
  imported: number;
  failed: BulkImportItemFailure[];
}

// Error Types

export class BookmarkNotFoundError extends Error {
  constructor(public readonly bookmarkId: string) {
    super(`Bookmark not found: '${bookmarkId}'`);
    this.name = "BookmarkNotFoundError";
  }
}

export class DuplicateBookmarkUrlError extends Error {
  constructor(public readonly url: string) {
    super(`Duplicate bookmark URL for user: '${url}'`);
    this.name = "DuplicateBookmarkUrlError";
  }
}

export class InvalidUrlError extends Error {
  constructor(public readonly url: string, public readonly reason: string) {
    super(`Invalid URL '${url}': ${reason}`);
    this.name = "InvalidUrlError";
  }
}

export class TagLimitExceededError extends Error {
  constructor(public readonly limit: number) {
    super(`Tag limit exceeded: maximum ${limit} tags per bookmark`);
    this.name = "TagLimitExceededError";
  }
}

export class UrlValidationTimeoutError extends Error {
  constructor(public readonly url: string) {
    super(`URL validation timed out for '${url}'`);
    this.name = "UrlValidationTimeoutError";
  }
}

export class StorageUnavailableError extends Error {
  constructor(message = "Bookmark storage is unavailable") {
    super(message);
    this.name = "StorageUnavailableError";
  }
}

// Interfaces

export interface BookmarkManager {
  createBookmark(userId: string, input: CreateBookmarkInput): Promise<Bookmark>;
  listBookmarks(userId: string, filter?: BookmarkFilter): Promise<Bookmark[]>;
  updateBookmark(
    userId: string,
    id: string,
    input: UpdateBookmarkInput
  ): Promise<Bookmark>;
  deleteBookmark(userId: string, id: string): Promise<void>;
  bulkImport(userId: string, urls: string[]): Promise<BulkImportResult>;
}

export interface TagService {
  normalizeTags(tags: string[]): Promise<string[]>;
  validateTagCount(tags: string[]): void;
}
