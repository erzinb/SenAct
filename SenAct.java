package senact.erzin.si;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.logging.Level;
import java.util.logging.Logger;

public class SenAct {

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
        Connection con = null;
        Statement st = null;
        ResultSet rs = null;

        String url = "jdbc:mysql://localhost:3306/senact";
        String user = "boris";
        String password = "tejkica00";

        try {
                Class.forName("com.mysql.jdbc.Driver");
            con = DriverManager.getConnection(url, user, password);
            System.out.println(System.currentTimeMillis()-cur);
            st = con.createStatement();
 //           rs = st.executeQuery("SELECT VERSION()");
            rs = st.executeQuery("SELECT * from activators");

            while (rs.next()) {
            	
                System.out.println(rs.getString(3));
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

}
