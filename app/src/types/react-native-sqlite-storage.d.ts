declare module 'react-native-sqlite-storage' {
  export interface ResultSet {
    rows: {
      item(index: number): any;
      length: number;
    };
    rowsAffected: number;
    insertId: number;
  }

  export interface Transaction {
    executeSql(
      sqlStatement: string,
      arguments?: any[],
      success?: (transaction: Transaction, resultSet: ResultSet) => void,
      error?: (transaction: Transaction, error: any) => void
    ): void;
  }

  export interface SQLiteDatabase {
    transaction(
      callback: (transaction: Transaction) => void,
      error?: (error: any) => void,
      success?: () => void
    ): Promise<void>;
    executeSql(
      sqlStatement: string,
      arguments?: any[],
      success?: (resultSet: ResultSet) => void,
      error?: (error: any) => void
    ): Promise<[ResultSet]>;
    close(): Promise<void>;
  }

  export function openDatabase(
    params: {
      name: string;
      location?: string;
      createFromLocation?: any;
    },
    success?: () => void,
    error?: (error: any) => void
  ): SQLiteDatabase;

  export function enablePromise(enable: boolean): void;

  const SQLite: {
    openDatabase: typeof openDatabase;
    enablePromise: typeof enablePromise;
  };

  export default SQLite;
}
