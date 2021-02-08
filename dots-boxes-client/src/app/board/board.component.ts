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

  moves : String[] = [];

  constructor(public boardService: BoardService) {
    for (let i = 0; i < this.boardService.rowNumber; i++) {
      this.stateMatrix[i] = [];
      for (let j = 0; j < this.boardService.colNumber; j++) {
        this.stateMatrix[i][j] = (new Square(false, false, false, false));
      }
    }

    this.height = (100 / this.boardService.rowNumber) + "%";
    this.width = (100 / this.boardService.colNumber) + "%";
    this.pobeda = Math.floor(((this.boardService.rowNumber) * (this.boardService.colNumber)) / 2);
    console.log(this.pobeda);
  }

  horizontalClick(Col: number, firstRow: number, secondRow: number) {
    const player = this.isFirstPlayer ? "Igrac : " : "AI : "
    this.moves.push(player + "Selektovano polje se nalazi u " + Col + " koloni, " + firstRow + " i " + secondRow + " redu.");

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
        this.setScore(true);
        provera = true;
      }
      else if (cloneMatricaStanja[secondRow][Col].setInnerDiv(this.isFirstPlayer) && !cloneMatricaStanja[firstRow][Col].setInnerDiv(this.isFirstPlayer)
        || !cloneMatricaStanja[secondRow][Col].setInnerDiv(this.isFirstPlayer) && cloneMatricaStanja[firstRow][Col].setInnerDiv(this.isFirstPlayer)) {
        provera = true;
      }
    }
    this.stateMatrix = cloneMatricaStanja;
    this.setScore(provera);
    if (!this.isFirstPlayer && this.boardService.selectedOponent === oponentType.AI && this.score2 <= this.pobeda) {
      this.AIMove();
    }
  }

  verticalClick(Row: number, firstCol: number, secondCol: number) {
    const player = this.isFirstPlayer ? "Igrac : " : "AI : "
    this.moves.push(player + "Selektovano polje se nalazi u: " + Row + " redu, " + firstCol + " i " + secondCol + " koloni.");

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
    if (!this.isFirstPlayer && this.boardService.selectedOponent === oponentType.AI && this.score2 <= this.pobeda) {
      this.AIMove();
    }
  }

  AIMove() {
    var isResponse = false
    const subscription = this.boardService.request(this.stateMatrix).subscribe(response => {
      console.log(response);
      switch (response.charAt(2)) {
        case "v":
          isResponse = true;
          this.verticalClick(parseInt(response.charAt(0)), parseInt(response.charAt(1)) - 1, parseInt(response.charAt(1)));
          break;
        case "h":
          isResponse = true;
          this.horizontalClick(parseInt(response.charAt(1)), parseInt(response.charAt(0)) - 1, parseInt(response.charAt(0)));
          break;
      }
      if(isResponse){
        subscription.unsubscribe();
      }
    });
  }

  setScore(check: boolean) {
    if (check) {
      if (this.isFirstPlayer) {
        this.moves.push("IGRAC JE UZEO POEN!");
        this.score1 += 1;
      }
      else {
        this.moves.push("AI JE UZEO POEN!");
        this.score2 += 1;
      }
    }
    else {
      this.isFirstPlayer = !this.isFirstPlayer;
    }
  }

  get getPlayer() {
    if (this.isFirstPlayer) {
      if (this.score1 > this.pobeda) {
        return "1. IGRAC JE POBEDIO!"
      }
      else {
        return "1. Igrac je na redu";
      }
    }
    else {
      if (this.score2 > this.pobeda) {
        return this.boardService.selectedOponent == oponentType.Player ? "2. IGRAC JE POBEDIO!" : "AI JE POBEDIO!"; 
      }
      else {
        return this.boardService.selectedOponent == oponentType.Player ? "2. igrac je na redu" : "AI je na redu";
      }
    }
  }
}