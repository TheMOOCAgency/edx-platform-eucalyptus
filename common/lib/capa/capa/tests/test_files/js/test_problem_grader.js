// Generated by CoffeeScript 1.6.1
(function() {
  var TestProblemGrader, root,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  TestProblemGrader = (function(_super) {

    __extends(TestProblemGrader, _super);

    function TestProblemGrader(submission, problemState, parameters) {
      this.submission = submission;
      this.problemState = problemState;
      this.parameters = parameters != null ? parameters : {};
      TestProblemGrader.__super__.constructor.call(this, this.submission, this.problemState, this.parameters);
    }

    TestProblemGrader.prototype.solve = function() {
      return this.solution = {
        0: this.problemState.value
      };
    };

    TestProblemGrader.prototype.grade = function() {
      var allCorrect, id, value, valueCorrect, _ref;
      if (this.solution == null) {
        this.solve();
      }
      allCorrect = true;
      _ref = this.solution;
      for (id in _ref) {
        value = _ref[id];
        valueCorrect = this.submission != null ? value === this.submission[id] : false;
        this.evaluation[id] = valueCorrect;
        if (!valueCorrect) {
          allCorrect = false;
        }
      }
      return allCorrect;
    };

    return TestProblemGrader;

  })(XProblemGrader);

  root = typeof exports !== "undefined" && exports !== null ? exports : this;

  root.graderClass = TestProblemGrader;

}).call(this);
