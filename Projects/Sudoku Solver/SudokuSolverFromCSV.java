import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public class SudokuSolverFromCSV {
    private static int GRID_SIZE = 9;


    public static void main(String[] args){

        String path = "/Users/kdmor/Documents/GitHub/Kevin-Morris-Portfolio/Projects/Sudoku Solver/SudokuBoard.csv";
        String line = "";

        int[][] board= new int[9][9];

        try {
            BufferedReader br = new BufferedReader(new FileReader(path));

            int i=0;

            while((line = br.readLine()) != null) {
                String[] values = line.split(",");
                for (int j=0; j<9; j++){
                    board[i][j] = Integer.parseInt(values[j]);                }
                i++;
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        printBoard(board);

        if (solveBoard(board)){
            System.out.println("SUCCESS");
        } else {
            System.out.println("Unsolveable");
        }

        printBoard(board);
    }

    private static void printBoard(int[][] board){
        for (int row=0; row<GRID_SIZE;row++){
            if (row%3 == 0 && row != 0){
                System.out.println("----------------------------------");
            }
            for (int column=0;column<GRID_SIZE;column++){
                if (column%3 == 0 && column!=0){
                    System.out.print(" |  ");
                }
                System.out.print(board[row][column] + "  ");
            }
            System.out.println();
        }
    }

    private static boolean isNumberInRow(int[][] board, int number, int row){
        for (int i=0;i<GRID_SIZE;i++){
            if (board[row][i]==number){
                return true;
            }
        }
        return false;
    }

    private static boolean isNumberInColumn(int[][] board, int number, int column){
        for (int i=0;i<GRID_SIZE;i++){
            if (board[i][column]==number){
                return true;
            }
        }
        return false;
    }

    private static boolean isNumberInBox(int[][] board, int number, int row, int column){
        int localBoxRow = row - (row%3);
        int localBoxColumn = column - (column%3);
        
        for (int i=localBoxRow; i<localBoxRow+3; i++){
            for (int j = localBoxColumn;j<localBoxColumn+3;j++){
                if (board[i][j] == number){
                    return true;
                }
            }
        }
        return false;
    }

    private static boolean isValidPlacement(int[][] board, int number, int row, int column){
        return !isNumberInRow(board, number, row) && !isNumberInColumn(board, number, column) && !isNumberInBox(board, number, row, column);
    }

    private static boolean solveBoard(int[][] board){
        for (int row = 0; row<GRID_SIZE; row++){
            for (int column = 0; column<GRID_SIZE; column++){
                if (board[row][column] == 0){
                    for (int numberToTry = 1; numberToTry<=GRID_SIZE; numberToTry++){
                        if (isValidPlacement(board, numberToTry, row, column)){
                            board[row][column] = numberToTry;

                            if (solveBoard(board)){
                                return true;
                            } else {
                                board[row][column] = 0;
                            }
                        }
                    }
                    return false;
                }
            }
        }
        return true;
    }


}
