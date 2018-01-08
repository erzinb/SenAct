package senact.erzin.si;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.LinkedList;
import java.util.List;
import java.util.Vector;
import java.util.Queue;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.pi4j.io.gpio.GpioController;
import com.pi4j.io.gpio.GpioFactory;
import com.pi4j.io.gpio.GpioPinDigitalMultipurpose;
import com.pi4j.io.gpio.RaspiPin;
import com.pi4j.io.gpio.event.GpioPinDigitalStateChangeEvent;
import com.pi4j.io.gpio.event.GpioPinListener;
import com.pi4j.io.gpio.event.GpioPinListenerDigital;
import com.pi4j.io.gpio.PinMode;
import com.pi4j.io.gpio.PinState;

public class SenAct {

	private static long exectime=0;
	private static long exectime2=0;
    private static Connection con = null;
    private static Statement st = null;
	private static ResultSet rs = null;
	private static List<Float> T1 = new LinkedList<Float>();
	private static List<Float> T2 = new LinkedList<Float>();
	private static final short N=30;
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		long cur = System.currentTimeMillis();
		long miliseconds = 0L;
		if(args.length > 0)
			miliseconds = 1000L * Integer.getInteger(args[0]).longValue();
		
		try {
			Thread.sleep(miliseconds);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

        String url = "jdbc:mysql://localhost:3306/senact";
        String user = "boris";
        String password = "tejkica00";

        try {
                Class.forName("com.mysql.jdbc.Driver");
            con = DriverManager.getConnection(url, user, password);
 //           System.out.println(System.currentTimeMillis()-cur);
            st = con.createStatement();
 //           rs = st.executeQuery("SELECT VERSION()");
 //           rs = st.executeQuery("SELECT * from sensors");

 /*           while (rs.next()) {
            	
                System.out.println(rs.getString(2));
            }
*/
            final GpioController gpio = GpioFactory.getInstance();
            
            final GpioPinDigitalMultipurpose pin1 = gpio.provisionDigitalMultipurposePin(RaspiPin.GPIO_13, PinMode.DIGITAL_OUTPUT);
    		
            pin1.addListener(new GpioPinListenerDigital() {
    			
    			@Override
    			public void handleGpioPinDigitalStateChangeEvent(
    					GpioPinDigitalStateChangeEvent event) {
    				// TODO Auto-generated method stub
    				
    				if(event.getState()==PinState.HIGH)
    				{
    					try {
    						long t=System.currentTimeMillis();
    						long dt=t-exectime;
//						System.out.println("Time elapsed for senzor1: " + dt);
    						pin1.setMode(PinMode.DIGITAL_OUTPUT);
    						pin1.low();
    						ResultSet rs = st.executeQuery("select k,n from sensors where id=1");
    						if(rs.next()) {
    							Float k=rs.getFloat("k");
    							Float n=rs.getFloat("n");
    							float T=(float)dt*k+n;

    							T1.add(T);
    							if(T1.size()>N)
    								T1.remove(0);
    							for(int i=0;i<T1.size();i++)
    							{
    								T+=T1.get(i);
    							}
    							T/=T1.size();
    							T = (float)(((int) (T*2)))/2;
    						   						
//    					System.out.println("Temperatura1: " + T);
    							int result = st.executeUpdate("update sensors set T="+T+" where id=1");
    						}
    					} catch (SQLException e) {
    						// TODO Auto-generated catch block
    						e.printStackTrace();
    					}
    				}
//                    System.out.println(" --> GPIO PIN STATE CHANGE: " + event.getPin() + " = " + event.getState());
    			}
    		});
            
            final GpioPinDigitalMultipurpose pin2 = gpio.provisionDigitalMultipurposePin(RaspiPin.GPIO_14, PinMode.DIGITAL_OUTPUT);
            pin2.addListener(new GpioPinListenerDigital() {
    			
    			@Override
    			public void handleGpioPinDigitalStateChangeEvent(
    					GpioPinDigitalStateChangeEvent event) {
    				// TODO Auto-generated method stub
    				
    				if(event.getState()==PinState.HIGH)
    				{
    					try {
    						long t=System.currentTimeMillis();
    						long dt=t-exectime2;
//    					System.out.println("Time elapsed for senzor2: " + dt);
    						pin2.setMode(PinMode.DIGITAL_OUTPUT);
    						pin2.low();
    						ResultSet rs = st.executeQuery("select k,n from sensors where id=2");
    						if(rs.next()) {
    							Float k=rs.getFloat("k");
    							Float n=rs.getFloat("n");
    							float T=(float)dt*k+n;
    							T2.add(T);
    							if(T2.size()>N)
    								T2.remove(0);
    							for(int i=0;i<T2.size();i++)
    							{
    								T+=T2.get(i);
    							}
    							T/=T2.size();
    							T = ((float)((int) (T*2)))/2;
    						
//    					System.out.println("Temperatura2: " + T);
    							int result = st.executeUpdate("update sensors set T="+T+" where id=2");
    						}
    					} catch (SQLException e) {
    						// TODO Auto-generated catch block
    						e.printStackTrace();
    					}
     				}
    			}
    		});

            // stop all GPIO activity/threads by shutting down the GPIO controller
            // (this method will forcefully shutdown all GPIO monitoring threads and scheduled tasks)
//            gpio.shutdown();

            while(true){
            	try {
                	pin1.setMode(PinMode.DIGITAL_OUTPUT);
                	pin1.low();
    				Thread.sleep(100);
    				pin1.setMode(PinMode.DIGITAL_INPUT);
    				exectime=System.currentTimeMillis();
    				Thread.sleep(400);
    				pin2.setMode(PinMode.DIGITAL_OUTPUT);
    				pin2.low();
    				Thread.sleep(100);
    				pin2.setMode(PinMode.DIGITAL_INPUT);
    				exectime2=System.currentTimeMillis();
    				Thread.sleep(400);
    			} catch (InterruptedException e) {
    				// TODO Auto-generated catch block
    				e.printStackTrace();
    			}
            }
        } catch (SQLException ex) {
            Logger lgr = Logger.getLogger(SenAct.class.getName());
            lgr.log(Level.SEVERE, ex.getMessage(), ex);

        } catch (ClassNotFoundException e) {
            Logger lgr = Logger.getLogger(SenAct.class.getName());
            lgr.log(Level.SEVERE, e.getMessage(), e);
			e.printStackTrace();
		} finally {
            try {
                if (rs != null) {
                    rs.close();
                }
                if (st != null) {
                    st.close();
                }
                if (con != null) {
                    con.close();
                }

            } catch (SQLException ex) {
                Logger lgr = Logger.getLogger(SenAct.class.getName());
                lgr.log(Level.WARNING, ex.getMessage(), ex);
            }
        }

	}

    /* (non-Javadoc)
	 * @see java.lang.Object#finalize()
	 */
	@Override
	protected void finalize() throws Throwable {
		// TODO Auto-generated method stub
		super.finalize();
        if (rs != null) {
            rs.close();
        }
        if (st != null) {
            st.close();
        }
		if(con!=null)
			con.close();
	}

}
