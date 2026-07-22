#nzlum {
  ::shape {
    polygon-opacity: 0.715;
    line-color: #232323;
    line-width: 0.26;
    line-opacity: 0.1;

    /* General unspecified/nulled category */
    [lu_code='NULL'] {
      polygon-fill: #fdffa6;
      polygon-opacity: 0.2;
    }

    // 1.1.1 Strict nature reserve
    [lu_code = '1.1.1'] {
      polygon-fill: #5E3A98;
    }

    // 1.1.2 Wilderness area
    [lu_code = '1.1.2'] {
      polygon-fill: #3F007D;
    }

    // 1.1.3 National Park
    [lu_code = '1.1.3'] {
      polygon-fill: #7C76B6;
    }

    // 1.1.4 Natural feature protection
    [lu_code = '1.1.4'] {
      polygon-fill: #A39FCB;
    }

    // 1.1.5 Habitat or species management area
    [lu_code = '1.1.5'] {
      polygon-fill: #C9CAE3;
    }

    // 1.1.6 Protected landscape
    [lu_code = '1.1.6'] {
      polygon-fill: #E9E8F2;
    }

    // 1.1.7 Other conserved area
    [lu_code = '1.1.7'] {
      polygon-fill: #FCFBFD;
    }

    // 1.2.0 Cultural and natural heritage
    [lu_code = '1.2.0'] {
      polygon-fill: #A00019;
    }

    // 1.3.0 Minimal use from relatively natural environments
    [lu_code = '1.3.0'] {
      polygon-fill: #FFC77A;
    }

    // 1.3.6 Defence land
    [lu_code = '1.3.6'] {
      polygon-fill: #FF9E17;
    }

    // 1.4.0 Unused land and land in transition
    [lu_code = '1.4.0'] {
      polygon-fill: #C8C69F;
    }

    // 2.1.0 Plantation forests
    [lu_code = '2.1.0'] {
      polygon-fill: #122112;
    }

    // 2.2.0 Grazing modified pasture systems
    [lu_code = '2.2.0'] {
      polygon-fill: #357735;
    }

    // 2.3.0 Short-rotation and seasonal cropping
    [lu_code = '2.3.0'] {
      polygon-fill: #7F7F54;
    }

    // 2.4.0 Perennial horticulture
    [lu_code = '2.4.0'] {
      polygon-fill: #A4A898;
    }

    // 2.5.0 Intensive horticulture
    [lu_code = '2.5.0'] {
      polygon-fill: #4A4C39;
    }

    // 2.6.0 Intensive animal production
    [lu_code = '2.6.0'] {
      polygon-fill: #BFA798;
    }

    // 2.7.0 Water and wastewater
    [lu_code = '2.7.0'] {
      polygon-fill: #3B505B;
    }

    // 2.8.0 Land in transition
    [lu_code = '2.8.0'] {
      polygon-fill: #BCBFE1;
    }

    // 3.1.0 Residential
    [lu_code = '3.1.0'] {
      polygon-fill: #815E5B;
    }

    // 3.2.0 Public recreation and services
    [lu_code = '3.2.0'] {
      polygon-fill: #C19878;
    }

    // 3.3.0 Commercial
    [lu_code = '3.3.0'] {
      polygon-fill: #B8C2CE;
    }

    // 3.4.0 Manufacturing and industrial
    [lu_code = '3.4.0'] {
      polygon-fill: #D0D2DF;
    }

    // 3.5.0 Utilities
    [lu_code = '3.5.0'] {
      polygon-fill: #F8ADFA;
    }

    // 3.6.0 Transport and communication
    [lu_code = '3.6.0'] {
      polygon-fill: #72737E;
    }

    // 3.7.0 Mining
    [lu_code = '3.7.0'] {
      polygon-fill: #E1CEA7;
    }

    // 3.8.0 Waste treatment and disposal
    [lu_code = '3.8.0'] {
      polygon-fill: #E77148;
    }

    // 3.9.0 Vacant and transitioning land
    [lu_code = '3.9.0'] {
      polygon-fill: #D69B97;
    }

    /* Water features, other than ice or wetlands (below) */
    [water!=''][water!='ice'][water!='swamp'][water!='mangrove'] {
      polygon-fill: #43a2ca;
    }

    /* Wetlands - coloured separately, matching wtr:swamp/wtr:mangrove
       in rdf/term-lists/water-features.ttl */
    [water='swamp'], [water='mangrove'] {
      polygon-fill: #83B09E;
    }

    /* Slightly emphasise parcels with a recorded commodity */
    [commod!=''] {
      polygon-opacity: 0.95;
    }
  }

  ::label {
    [zoom>14] {
      text-name: [comment];
      text-face-name: 'Open Sans Regular';
      text-avoid-edges: true;
      text-allow-overlap: false;
      text-character-spacing: 0.5;
      text-size: 12;
      text-fill: #fff;
      text-halo-fill: fadeout(black, 40%);
      text-halo-radius: 1;
    }
  }
}
