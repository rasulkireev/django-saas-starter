import "../styles/index.css";

import { Application } from "@hotwired/stimulus";
import { definitionsFromContext } from "@hotwired/stimulus-webpack-helpers";

import Dropdown from '@stimulus-components/dropdown';

const application = Application.start();

const context = require.context("../controllers", true, /\.js$/);
application.load(definitionsFromContext(context));

application.register('dropdown', Dropdown);
