import SQLite, { SQLiteDatabase } from 'react-native-sqlite-storage';

SQLite.enablePromise(true);

const database_name = "MosaicAlert.db";

export interface ScanRecord {
  id?: number;
  timestamp: string;
  prediction: string;
  confidence: number;
  imagePath: string;
  isSynced: number;
}

class DatabaseService {
  private db: SQLiteDatabase | null = null;

  async initDB() {
    if (this.db) return this.db;

    try {
      this.db = await SQLite.openDatabase({
        name: database_name,
        location: 'default',
      });

      await this.createTable();
      return this.db;
    } catch (error) {
      console.error("Database initialization error:", error);
      throw error;
    }
  }

  private async createTable() {
    if (!this.db) return;
    
    await this.db.executeSql(`
      CREATE TABLE IF NOT EXISTS Scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        prediction TEXT,
        confidence REAL,
        imagePath TEXT,
        isSynced INTEGER DEFAULT 0
      );
    `);
  }

  async saveScan(scan: ScanRecord) {
    const db = await this.initDB();
    const query = `
      INSERT INTO Scans (timestamp, prediction, confidence, imagePath, isSynced)
      VALUES (?, ?, ?, ?, ?);
    `;
    const params = [scan.timestamp, scan.prediction, scan.confidence, scan.imagePath, scan.isSynced];
    
    try {
      const [results] = await db.executeSql(query, params);
      return results.insertId;
    } catch (error) {
      console.error("Failed to save scan:", error);
      throw error;
    }
  }

  async getHistory(): Promise<ScanRecord[]> {
    const db = await this.initDB();
    try {
      const [results] = await db.executeSql('SELECT * FROM Scans ORDER BY timestamp DESC;');
      const history: ScanRecord[] = [];
      for (let i = 0; i < results.rows.length; i++) {
        history.push(results.rows.item(i));
      }
      return history;
    } catch (error) {
      console.error("Failed to fetch history:", error);
      return [];
    }
  }

  async deleteScan(id: number) {
    const db = await this.initDB();
    await db.executeSql('DELETE FROM Scans WHERE id = ?;', [id]);
  }
}

export default new DatabaseService();
