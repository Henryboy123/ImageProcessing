import ij.*;
import ij.process.*;
import ij.plugin.*;

import java.awt.*;
import java.io.*;
import java.util.*;

public class task1 implements PlugIn {
    public void run(String arg) {
        int imageWidth = 181;
        int imageHeight = 181;

        ByteProcessor binaryProcessor = new ByteProcessor(imageWidth, imageHeight);
        binaryProcessor.setColor(255);
        binaryProcessor.fill();

        String filePath = "/home/hynrikhop/Documents/Obsidian Vault/AUA/Image Processing/HW1/yor-f-83.stu";
        try {
            File inputFile = new File(filePath);
            Scanner fileScanner = new Scanner(inputFile);
            String line;

            while (fileScanner.hasNextLine()) {
                line = fileScanner.nextLine().trim();
                String[] tokens = line.split(" ");

                

                int i = 0;
                while (i < tokens.length - 2) {
                    int xCoordinate = (int) Double.parseDouble(tokens[i]);
                    int yCoordinate = (int) Double.parseDouble(tokens[i + 1]);

                    binaryProcessor.set(xCoordinate, yCoordinate, 0);
                    binaryProcessor.set(yCoordinate, xCoordinate, 0);

                    i += 2; // Move to the next pair of coordinates
                }
            }

            ImagePlus resultImage = new ImagePlus("Image", binaryProcessor);
            resultImage.show();
            fileScanner.close();
        } catch (Exception e) {
            IJ.log("Error reading the file: " + e.getMessage());
        }
    }
}

