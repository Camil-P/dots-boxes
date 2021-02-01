import { Component } from '@angular/core';
import { BoardService, oponentType } from '../services/board.service';
import { Square } from '../type';

@Component({
  selector: 'app-board',
  templateUrl: './board.component.html',
  styleUrls: ['./board.component.css']
})
export class BoardComponent {
  height: string = "";
  width: string = "";

  pobeda: number = 0;

  score1: number = 0;
  score2: number = 0;

  isFirstPlayer: boolean = true;

  stateMatrix: Square[][] = [];

  constructor(public boardService: BoardService) {
    for (let i = 0; i < this.boardService.rowNumber; i++) {
      this.stateMatrix[i] = [];
      for (let j = 0; j < this.boardService.colNumber; j++) {
        this.stateMatrix[i][j] = (new Square(false, false, false, false));
      }
    }

    this.height = (100 / this.boardService.rowNumber) + "%";
    this.width = (100 / this.boardService.colNumber) + "%";
    this.pobeda = ((this.boardService.rowArray.length - 1) * (this.boardService.columnArray.length - 1)) / 2 + 1;
  }

  horizontalClick(Col: number, firstRow: number, secondRow: number) {
    console.log("Selektovane kocke se nalaze u " + Col + " koloni i " + firstRow + " i " + secondRow + " redu.");

    var provera = false;
    const cloneMatricaStanja = [...this.stateMatrix];

    if (firstRow < 0) {
      cloneMatricaStanja[secondRow][Col].top = true;
      cloneMatricaStanja[secondRow][Col].clickedSides += 1;
      if (cloneMatricaStanja[secondRow][Col].setInnerDiv(this.isFirstPlayer)) {
        provera = true;
      }
    }
    else if (secondRow > (this.boardService.rowArray.length - 2)) {
      cloneMatricaStanja[firstRow][Col].bottom = true;
      cloneMatricaStanja[firstRow][Col].clickedSides += 1;
      if (cloneMatricaStanja[firstRow][Col].setInnerDiv(this.isFirstPlayer)) {
        provera = true
      }
    }
    else {
      cloneMatricaStanja[firstRow][Col].bottom = true;
      cloneMatricaStanja[secondRow][Col].top = true;
      cloneMatricaStanja[firstRow][Col].clickedSides += 1;
      cloneMatricaStanja[secondRow][Col].clickedSides += 1;
      if (cloneMatricaStanja[secondRow][Col].setInnerDiv(this.isFirstPlayer) && cloneMatricaStanja[firstRow][Col].setInnerDiv(this.isFirstPlayer)) {
        provera = true;
      }
      else if (cloneMatricaStanja[secondRow][Col].setInnerDiv(this.isFirstPlayer) && !cloneMatricaStanja[firstRow][Col].setInnerDiv(this.isFirstPlayer)
        || !cloneMatricaStanja[secondRow][Col].setInnerDiv(this.isFirstPlayer) && cloneMatricaStanja[firstRow][Col].setInnerDiv(this.isFirstPlayer)) {
        provera = true;
      }
    }
    this.stateMatrix = cloneMatricaStanja;
    this.setScore(provera);
    if (!this.isFirstPlayer && this.boardService.selectedOponent === oponentType.AI) {
      this.AIMove();
    }
  }

  verticalClick(Row: number, firstCol: number, secondCol: number) {
    console.log("Selektovane kocke se nalaze u " + Row + " redu i " + firstCol + " i " + secondCol + " koloni.");

    var provera = false;
    const cloneMatricaStanja = [...this.stateMatrix];

    if (firstCol < 0) {
      cloneMatricaStanja[Row][secondCol].left = true;
      cloneMatricaStanja[Row][secondCol].clickedSides += 1;
      if (cloneMatricaStanja[Row][secondCol].setInnerDiv(this.isFirstPlayer)) {
        provera = true;
      }
    }
    else if (secondCol > (this.boardService.columnArray.length - 2)) {
      cloneMatricaStanja[Row][firstCol].right = true;
      cloneMatricaStanja[Row][firstCol].clickedSides += 1;
      if (cloneMatricaStanja[Row][firstCol].setInnerDiv(this.isFirstPlayer)) {
        provera = true;
      }
    }
    else {
      cloneMatricaStanja[Row][firstCol].right = true;
      cloneMatricaStanja[Row][secondCol].left = true;
      cloneMatricaStanja[Row][firstCol].clickedSides += 1;
      cloneMatricaStanja[Row][secondCol].clickedSides += 1;
      if (cloneMatricaStanja[Row][secondCol].setInnerDiv(this.isFirstPlayer) && cloneMatricaStanja[Row][firstCol].setInnerDiv(this.isFirstPlayer)) {
        this.setScore(true);
        provera = true;
      }
      else if (cloneMatricaStanja[Row][secondCol].setInnerDiv(this.isFirstPlayer) && !cloneMatricaStanja[Row][firstCol].setInnerDiv(this.isFirstPlayer)
        || !cloneMatricaStanja[Row][secondCol].setInnerDiv(this.isFirstPlayer) && cloneMatricaStanja[Row][firstCol].setInnerDiv(this.isFirstPlayer)) {
        provera = true;
      }
    }
    this.stateMatrix = cloneMatricaStanja;
    this.setScore(provera);
    if (!this.isFirstPlayer && this.boardService.selectedOponent === oponentType.AI) {
      this.AIMove();
    }
  }

  AIMove() {
    const subscription = this.boardService.request(this.stateMatrix).subscribe(response => {
      switch (response.side) {
        case "v":
          this.verticalClick(response.i, response.j - 1, response.j);
          break;
        case "h":
          this.horizontalClick(response.j, response.i - 1, response.i);
          break;
        default:
          console.log(response);
          break;
      }

    });
    subscription.unsubscribe();
  }

  setScore(check: boolean) {
    if (check) {
      if (this.isFirstPlayer) {
        this.score1 += 1;
      }
      else {
        this.score2 += 1;
      }
    }
    else {
      this.isFirstPlayer = !this.isFirstPlayer;
    }
  }

  get getPlayer() {
    if (this.isFirstPlayer) {
      if (this.score1 >= this.pobeda) {
        return "1. IGRAC JE POBEDIO!"
      }
      else {
        return "1. Igrac je na redu";
      }
    }
    else {
      if (this.score2 >= this.pobeda) {
        return "2. IGRAC JE POBEDIO!"
      }
      else {
        return "2. Igrac je na redu";
      }
    }
  }
}
