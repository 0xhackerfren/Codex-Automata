/**
 * SDK Constraint Surface: Task Manager
 *
 * These types and interfaces define the building blocks that implementation
 * code must conform to. No implementation logic belongs in this file.
 *
 * Spec reference: docs/spec.md
 * Contract reference: docs/interface-contracts.md
 */

// Domain Types

export type TaskStatus = "pending" | "complete";

export interface Task {
  id: string;
  title: string;
  description: string;
  status: TaskStatus;
  created_at: Date;
  completed_at: Date | null;
}

export interface CreateTaskInput {
  title: string;
  description?: string;
}

export interface ListTasksFilter {
  status?: TaskStatus;
}

// Error Types

export class TaskNotFoundError extends Error {
  constructor(public readonly taskId: string) {
    super(`Task not found: no task exists with id '${taskId}'`);
    this.name = "TaskNotFoundError";
  }
}

export class TaskAlreadyCompleteError extends Error {
  constructor(public readonly taskId: string) {
    super(`Task already complete: task '${taskId}' has already been completed`);
    this.name = "TaskAlreadyCompleteError";
  }
}

export class InvalidTaskInputError extends Error {
  constructor(public readonly field: string, public readonly reason: string) {
    super(`Invalid input for '${field}': ${reason}`);
    this.name = "InvalidTaskInputError";
  }
}

// Interfaces

export interface TaskManager {
  createTask(input: CreateTaskInput): Promise<Task>;
  listTasks(filter?: ListTasksFilter): Promise<Task[]>;
  completeTask(id: string): Promise<Task>;
  deleteTask(id: string): Promise<void>;
}

export interface Storage {
  save(task: Task): Promise<void>;
  findById(id: string): Promise<Task | null>;
  findAll(filter?: ListTasksFilter): Promise<Task[]>;
  delete(id: string): Promise<boolean>;
}
