import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Square } from '../type';

interface Request {
  matrix: Square[][]
  mod: modType
}

@Injectable({
  providedIn: 'root'
})
export class BoardService {
  rowNumber: number = 4;
  colNumber: number = 4;

  rowArray: number[] = [];
  columnArray: number[] = [];

  selectedOponent = oponentType.AI;
  selectedMod = modType.hard;

  gameAvailable: boolean = false;

  baseUrl = 'http://127.0.0.1:8000/api/';
  constructor(private httpClient: HttpClient) { }

  createArrays() {
    for (let i = 0; i <= this.rowNumber; i++) {
      this.rowArray.push(i);
    }
    for (let i = 0; i <= this.colNumber; i++) {
      this.columnArray.push(i);
    }
  }

  request(stateMatrix: Square[][]): Observable<any> {
    const request : Request = { matrix: stateMatrix, mod: this.selectedMod };
    return this.httpClient.post<any>(this.baseUrl, request);
  }
}

export enum oponentType {
  Player = "vs Player",
  AI = "vs AI",
}

export enum modType {
  easy = "Easy",
  medium = "Medium",
  hard = "Hard",
}

