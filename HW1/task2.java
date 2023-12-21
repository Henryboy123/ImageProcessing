import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;

public class task2 implements PlugInFilter {

    @Override
    public int setup(String arg, ImagePlus imp) {
        return DOES_ALL;
    }

    @Override
    public void run(ImageProcessor ip) {
        int imageWidth = ip.getWidth();
        int imageHeight = ip.getHeight();

        int centerX = imageWidth / 2;
        int centerY = imageHeight / 2;

        ImageProcessor leftPanel = extractPanel(ip, 0, 0, centerX, imageHeight);
        ImageProcessor rightPanel = extractPanel(ip, centerX, 0, imageWidth - centerX, imageHeight);

        flipHorizontal(leftPanel);
        flipHorizontal(rightPanel);

        ImageProcessor topPanel = extractPanel(ip, 0, 0, imageWidth, centerY);
        ImageProcessor bottomPanel = extractPanel(ip, 0, centerY, imageWidth, imageHeight - centerY);

        flipVertical(topPanel);
        flipVertical(bottomPanel);

        ip.insert(leftPanel, 0, 0);
        ip.insert(rightPanel, centerX, 0);
        ip.insert(topPanel, 0, 0);
        ip.insert(bottomPanel, 0, centerY);
    }

    private ImageProcessor extractPanel(ImageProcessor ip, int x, int y, int width, int height) {
        ImageProcessor panel = ip.duplicate();
        panel.setRoi(x, y, width, height);
        return panel.crop();
    }

    private void flipHorizontal(ImageProcessor ip) {
        ip.flipHorizontal();
    }

    private void flipVertical(ImageProcessor ip) {
        ip.flipVertical();
    }
}

