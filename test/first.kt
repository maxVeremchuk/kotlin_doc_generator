import second
import sub.sub_first
import sub.sub_sub.sub_sub_first

/**
* first class desctiprion blah blah blah blah blah blah blah blah blah blah blah blah blah blah
*/
class first(p: Int) {

	constructor(x: String) : this(x) {
		Int a = 10;
	}
	/**
	* first_value_description blah blah blahblahblahblahblahblah
	*/
	var first_value: Int

	fun first_func(){
		val obj = second()
		obj.second_func()

		var obj1 = sub_first()
		obj1.sub_first_func()
	}

	/**
	* first_func_func_description blah blah blahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblah
	*/
	fun first_func_func(){
		val obj = sub_sub_first()
		obj.sub_sub_first_func()
	}
}