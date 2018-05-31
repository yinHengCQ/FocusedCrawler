import org.apache.commons.io.IOUtils;
import org.tensorflow.*;
import org.tensorflow.Shape;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.geom.AffineTransform;
import java.awt.image.AffineTransformOp;
import java.awt.image.BufferedImage;
import java.io.*;
import java.util.*;
import java.util.List;

public class test {
    private static Map<Long,String> index2StringMap=new HashMap<>();
    private static final String PBPATH="C:\\Users\\admin\\Desktop\\java_result\\graph.pb";

    static void init(){
        index2StringMap.put(0L,"0");
        index2StringMap.put(1L,"1");
        index2StringMap.put(2L,"2");
        index2StringMap.put(3L,"3");
        index2StringMap.put(4L,"4");
        index2StringMap.put(5L,"5");
        index2StringMap.put(6L,"6");
        index2StringMap.put(7L,"7");
        index2StringMap.put(8L,"8");
        index2StringMap.put(9L,"9");
        index2StringMap.put(36L,"a");
        index2StringMap.put(37L,"b");
        index2StringMap.put(38L,"c");
        index2StringMap.put(39L,"d");
        index2StringMap.put(40L,"e");
        index2StringMap.put(41L,"f");
        index2StringMap.put(42L,"g");
        index2StringMap.put(43L,"h");
        index2StringMap.put(44L,"i");
        index2StringMap.put(45L,"j");
        index2StringMap.put(46L,"k");
        index2StringMap.put(47L,"l");
        index2StringMap.put(48L,"m");
        index2StringMap.put(49L,"n");
        index2StringMap.put(50L,"o");
        index2StringMap.put(51L,"p");
        index2StringMap.put(52L,"q");
        index2StringMap.put(53L,"r");
        index2StringMap.put(54L,"s");
        index2StringMap.put(55L,"t");
        index2StringMap.put(56L,"u");
        index2StringMap.put(57L,"v");
        index2StringMap.put(58L,"w");
        index2StringMap.put(59L,"x");
        index2StringMap.put(60L,"y");
        index2StringMap.put(61L,"z");
        index2StringMap.put(10L,"A");
        index2StringMap.put(11L,"B");
        index2StringMap.put(12L,"C");
        index2StringMap.put(13L,"D");
        index2StringMap.put(14L,"E");
        index2StringMap.put(15L,"F");
        index2StringMap.put(16L,"G");
        index2StringMap.put(17L,"H");
        index2StringMap.put(18L,"I");
        index2StringMap.put(19L,"J");
        index2StringMap.put(20L,"K");
        index2StringMap.put(21L,"L");
        index2StringMap.put(22L,"M");
        index2StringMap.put(23L,"N");
        index2StringMap.put(24L,"O");
        index2StringMap.put(25L,"P");
        index2StringMap.put(26L,"Q");
        index2StringMap.put(27L,"R");
        index2StringMap.put(28L,"S");
        index2StringMap.put(29L,"T");
        index2StringMap.put(30L,"U");
        index2StringMap.put(31L,"V");
        index2StringMap.put(32L,"W");
        index2StringMap.put(33L,"X");
        index2StringMap.put(34L,"Y");
        index2StringMap.put(35L,"Z");
    }

    private static Color[][] img2color(BufferedImage bi){
        int width = bi.getWidth();
        int height = bi.getHeight();
        int minx = bi.getMinX();
        int miny = bi.getMinY();
        Color[][] allcolor=new Color[height-miny][width-minx];
        for (int j = miny; j < height; j++) {
            for (int i = minx; i < width; i++) {
                int pixel = bi.getRGB(i, j); // 下面三行代码将一个数字转换为RGB数字
                allcolor[j-miny][i-minx] = new Color(pixel);
            }
        }
        return allcolor;
    }

    private static List<Color> getTopColorList(Integer colorCount, BufferedImage bi){
        Color[][] color=img2color(bi);
        Map<Color,Integer> topColorSort=new HashMap<>();
        for (Color[]i:color) {
            for (Color j:i) {
                if ((j.getBlue()+j.getRed()+j.getGreen())<730){
                    if (topColorSort.get(j)==null) {
                        topColorSort.put(j, 1);
                    }else {
                        topColorSort.put(j,topColorSort.get(j)+1);
                    }
                }
            }
        }
        List<Map.Entry<Color,Integer>> topColorSortList=new ArrayList<>();
        for (Map.Entry<Color,Integer> var:topColorSort.entrySet()) {
            topColorSortList.add(var);
        }
        Collections.sort(topColorSortList, new Comparator<Map.Entry<Color, Integer>>() {
            @Override
            public int compare(Map.Entry<Color, Integer> o1, Map.Entry<Color, Integer> o2) {
                return o2.getValue()-o1.getValue();
            }
        });
        List<Color> result=new ArrayList<>();
        for (Map.Entry<Color, Integer> var:topColorSortList.subList(0,colorCount)) {
            result.add(var.getKey());
        }
        return result;
    }

    private static List<Color> getTop4Color(List<Color> topColorList,List<Color> result){
        Color temp=topColorList.remove(0);
        result.add(temp);
        if(result.size()==4){
            return result;
        }
        List<Color> needToRemove=new ArrayList<>();
        for (Color var:topColorList) {
            if((Math.abs(var.getRed()-temp.getRed())+Math.abs(var.getGreen()-temp.getGreen())+Math.abs(var.getBlue()-temp.getBlue()))<10){
                needToRemove.add(var);
            }
        }
        topColorList.removeAll(needToRemove);
        return getTop4Color(topColorList,result);
    }

    private static boolean isNearby(Set<int[][]> mainColor,Integer i,Integer j){
        for (int[][] var:mainColor) {
            if (Math.abs(var[0][0]-i)<3 && Math.abs(var[0][1]-j)<20){
                return true;
            }
        }
        return false;
    }

    private static Map<Integer,BufferedImage> cutPicByColor(Color specifyColor,BufferedImage bi, Map<Integer,BufferedImage> result) throws Exception {
        int width = bi.getWidth();
        int height = bi.getHeight();
        int minx = bi.getMinX();
        int miny = bi.getMinY();

        Set<int[][]> mainColor=new HashSet<>();
        Set<Integer> xPositions=new HashSet<>();
        Set<Integer> yPositions=new HashSet<>();
        for (int j = miny; j < height; j++) {
            for (int i = minx; i < width; i++) {
                int pixel = bi.getRGB(i, j); // 下面三行代码将一个数字转换为RGB数字
                Color temp = new Color(pixel);
                if(Math.abs(temp.getRed()-specifyColor.getRed())<10 && Math.abs(temp.getGreen()-specifyColor.getGreen())<10 && Math.abs(temp.getBlue()-specifyColor.getBlue())<10){
                    mainColor.add(new int[][]{{i,j}});
                    xPositions.add(i);
                    yPositions.add(j);
                }
            }
        }
        int left_top=Collections.min(xPositions);
        int left_down=Collections.min(yPositions);
        int cut_width=Collections.max(xPositions)-left_top;
        int cut_height=Collections.max(yPositions)-left_down;
        if(cut_width<15){
            left_top=left_top-6;
            cut_width=cut_width+12;
        }

        result.put(left_top, resizeImage(bi.getSubimage(left_top,left_down,cut_width,cut_height),45,45));
        return result;
    }

//    private static void pic2pics(List<Color> colorList, BufferedImage bi) throws Exception {
//        Map<Integer,BufferedImage> colorPositionMap=new HashMap<>();
//        for (int i = 0; i < colorList.size(); i++) {
//            BufferedImage temp=new BufferedImage(bi.getWidth(), bi.getHeight(), bi.getType());
//            temp.setData(bi.getData());
//            try {
//                cutPicByColor(colorList.get(i),temp,colorPositionMap);
//            } catch (Exception e) {
//                e.printStackTrace();
//            }
//        }
//        List<Map.Entry<Integer, BufferedImage>> colorPositionList=new ArrayList<>();
//        for (Map.Entry<Integer, BufferedImage> var:colorPositionMap.entrySet()) {
//            colorPositionList.add(var);
//        }
//        Collections.sort(colorPositionList, new Comparator<Map.Entry<Integer, BufferedImage>>() {
//
//            @Override
//            public int compare(Map.Entry<Integer, BufferedImage> o1, Map.Entry<Integer, BufferedImage> o2) {
//                return o1.getKey()-o2.getKey();
//            }
//        });
//
//        for (int i = 0; i <colorPositionList.size() ; i++) {
//            OutputStream output = new FileOutputStream(new File("C:\\Users\\admin\\Desktop\\outout\\out{0}.png".replace("{0}",UUID.randomUUID().toString())));
//            ImageIO.write(binaryImage(colorPositionList.get(i).getValue()), "png", output);
//        }
//    }

    private static List<Map.Entry<Integer, BufferedImage>> pic2picStreams(List<Color> colorList, BufferedImage bi) throws Exception {
        Map<Integer,BufferedImage> colorPositionMap=new HashMap<>();
        for (int i = 0; i < colorList.size(); i++) {
            BufferedImage temp=new BufferedImage(bi.getWidth(), bi.getHeight(), bi.getType());
            temp.setData(bi.getData());
            try {
                cutPicByColor(colorList.get(i),temp,colorPositionMap);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        List<Map.Entry<Integer, BufferedImage>> colorPositionList=new ArrayList<>();
        for (Map.Entry<Integer, BufferedImage> var:colorPositionMap.entrySet()) {
            colorPositionList.add(var);
        }
        Collections.sort(colorPositionList, new Comparator<Map.Entry<Integer, BufferedImage>>() {

            @Override
            public int compare(Map.Entry<Integer, BufferedImage> o1, Map.Entry<Integer, BufferedImage> o2) {
                return o1.getKey()-o2.getKey();
            }
        });
        return colorPositionList;
    }


    private static BufferedImage binaryImage(BufferedImage image) throws Exception {
        int w = image.getWidth();
        int h = image.getHeight();
        float[] rgb = new float[3];
        double[][] zuobiao = new double[w][h];
        int black = new Color(0, 0, 0).getRGB();
        int white = new Color(255, 255, 255).getRGB();
        BufferedImage bi= new BufferedImage(w, h,
                BufferedImage.TYPE_BYTE_BINARY);
        for (int x = 0; x < w; x++) {
            for (int y = 0; y < h; y++) {
                int pixel = image.getRGB(x, y);
                rgb[0] = (pixel & 0xff0000) >> 16;
                rgb[1] = (pixel & 0xff00) >> 8;
                rgb[2] = (pixel & 0xff);
                float avg = (rgb[0]+rgb[1]+rgb[2])/3;
                zuobiao[x][y] = avg;
            }
        }
        double SW = 192;
        for (int x = 0; x < w; x++) {
            for (int y = 0; y < h; y++) {
                if (zuobiao[x][y] < SW) {
                    bi.setRGB(x, y, black);
                }else{
                    bi.setRGB(x, y, white);
                }
            }
        }
        return bi;
    }

    private static BufferedImage resizeImage(BufferedImage orgin,int w,int h) throws Exception {
        double wr=w*1.0/orgin.getWidth();     //获取缩放比例
        double hr=h*1.0 / orgin.getHeight();
        AffineTransformOp ato = new AffineTransformOp(AffineTransform.getScaleInstance(wr, hr), null);
        return ato.filter(orgin, null);
    }

    private static float[] img2array(BufferedImage bi){
        float[] out=new float[2025];
        int index=0;
        for (int k = 0; k < bi.getHeight(); k++) {
            for (int i = 0; i < bi.getWidth(); i++) {
                Color temp=new Color(bi.getRGB(i,k));
                out[index]=temp.getRed()/255.0f;
                index++;
            }
        }
        return out;
    }

    private static String singlePic2text(BufferedImage bi) {
        try (Graph graph = new Graph()) {
            //导入图
            byte[] graphBytes = IOUtils.toByteArray(new FileInputStream(new File(PBPATH)));
            graph.importGraphDef(graphBytes);

            //根据图建立Session
            try(Session session = new Session(graph)){
//                Tensor<?> result= session.runner().feed(graph.operation("data-input").output(0),Tensor.create(new float[][]{img2array(ImageIO.read(new File("C:\\Users\\admin\\Desktop\\cutout\\390.jpg")))})).feed(graph.operation("keep-prob").output(0),Tensor.create(1.0f)).fetch(graph.operation("predict_max_idx").output(0)).run().get(0);
                Tensor<?> result= session.runner().feed(graph.operation("data-input").output(0),Tensor.create(new float[][]{img2array(bi)})).feed(graph.operation("keep-prob").output(0),Tensor.create(1.0f)).fetch(graph.operation("predict_max_idx").output(0)).run().get(0);
                return index2StringMap.get(result.copyTo(new long[1][1])[0][0]);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return "";
    }


    public static String pic2text(String filePath){
        String result="";
        try {
            BufferedImage bi=ImageIO.read(new File(filePath));
            List<Color> colorList=getTop4Color(getTopColorList(20,bi),new ArrayList<Color>());
//            pic2pics(colorList,bi);
            List<Map.Entry<Integer, BufferedImage>> picStreams=pic2picStreams(colorList,bi);
            for (int i = 0; i <picStreams.size() ; i++) {
                OutputStream output = new FileOutputStream(new File("C:\\Users\\admin\\Desktop\\outout\\out{0}.png".replace("{0}",Integer.valueOf(i).toString())));
                ImageIO.write(binaryImage(picStreams.get(i).getValue()), "png", output);
                result+=singlePic2text(picStreams.get(i).getValue());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return result;
    }

//    for (int i = 0; i <colorPositionList.size() ; i++) {
//        OutputStream output = new FileOutputStream(new File("C:\\Users\\admin\\Desktop\\outout\\out{0}.png".replace("{0}",Integer.valueOf(i).toString())));
//        ImageIO.write(binaryImage(colorPositionList.get(i).getValue()), "png", output);
//    }

    public static void main(String [] args){
        long start=System.currentTimeMillis();
        init();
//        String temp=pic2text("C:\\Users\\admin\\Desktop\\zhixing\\zhixing888.jpg");
//        System.out.println(temp);

        for (int i = 0; i < 50; i++) {
            System.out.println(String.valueOf(i)+"--"+pic2text("C:\\Users\\admin\\Desktop\\zhixing\\zhixing"+String.valueOf(i)+".jpg"));
        }

        System.out.println(System.currentTimeMillis()-start);
        

//        for (int i = 0; i < 600 ; i++) {
//            String pathName="C:\\Users\\admin\\Desktop\\color\\"+String.valueOf(i)+".jpg";
//            pic2text(pathName);
//        }
    }

}