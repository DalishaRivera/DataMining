package example.helloworld;

import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.Label;

import org.eclipse.swt.SWT;
import org.eclipse.swt.graphics.Image;
import org.eclipse.ui.part.ViewPart;

public class HelloWorldView extends ViewPart {
   Label label;
   Image image;
   public HelloWorldView() {
   }
   public void createPartControl(Composite parent) {
      label = new Label(parent, SWT.NONE);
      label.setText("Hello World");
      
      label = new Label(parent, SWT.NONE);
      image = new Image(null, "C:\\Users\\Dalisha\\Visualization\\"
				+ "example.HelloWorld\\SourceFolder\\HelloWorldRedImage.jpg");
	  label.setImage(image);
   }
   public void setFocus() {
	   
      // set focus to my widget.  For a label, this doesn't
      // make much sense, but for more complex sets of widgets
      // you would decide which one gets the focus.
   }
}

