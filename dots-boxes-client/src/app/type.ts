export class Square {

    top: boolean;
    bottom: boolean;
    left: boolean;
    right: boolean;
    clickedSides = 0;
    allSides= 0;

    constructor(t, b, l, r) {
        this.top = t;
        this.bottom = b;
        this.left = l;
        this.right = r;
    }

    setInnerDiv(move : boolean) : boolean{
        if(this.top === true && this.bottom === true && 
           this.left === true && this.right === true){
            this.allSides = move ? 1 : 2;
            return true;
        }
        return false;
    }
}
