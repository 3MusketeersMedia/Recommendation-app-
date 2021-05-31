import { useEffect } from 'react';
import { withRouter } from 'react-router-dom';

/*
  https://stackoverflow.com/questions/36904185/react-router-scroll-to-top-on-every-transition
  ScrollToTop component found from stack overflow
*/
function ScrollToTop({ history }) {
  useEffect(() => {
    const unlisten = history.listen(() => {
      window.scrollTo(0, 0);
    });
    return () => {
      unlisten();
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (null);
}

export default withRouter(ScrollToTop);
