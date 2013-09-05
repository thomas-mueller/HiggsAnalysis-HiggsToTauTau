#include "TGraph.h"

inline void
PlotLimits::arXiv_1211_6956(TGraph* graph)
{
  /* HIGG-2012-11 H->tautau search (4.8/fb)
     http://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/HIGG-2012-11/
  */
  graph->SetPoint( 0, 91.07692307692307   , 25.573333333333334 );
  graph->SetPoint( 1, 100.1628959276018   , 12.666666666666666 );
  graph->SetPoint( 2, 110.09954751131221  , 9.786666666666665  );
  graph->SetPoint( 3, 120.93212669683258  , 9.466666666666665  );
  graph->SetPoint( 4, 130.41628959276017  , 9.253333333333332  );
  graph->SetPoint( 5, 140.63348416289594  , 9.679999999999996  );
  graph->SetPoint( 6, 150.85972850678735  , 10.213333333333333 );
  graph->SetPoint( 7, 171.1945701357466   , 9.893333333333327  );
  graph->SetPoint( 8, 200.56108597285066  , 12.026666666666667 );
  graph->SetPoint( 9, 251.16742081447967  , 16.506666666666668 );
  graph->SetPoint(10, 301.0769230769231   , 20.773333333333333 );
  graph->SetPoint(11, 351.83710407239823  , 27.066666666666663 );
  graph->SetPoint(12, 402.64253393665166  , 33.89333333333333  );
  graph->SetPoint(13, 453.0226244343892   , 43.70666666666667  );
  graph->SetPoint(14, 504.31674208144796  , 56.29333333333334  );
}
  