<?php
class NavigatorItem
{
	private $id;
	private $text;
	private $url;
	private $subItems;
	
	function __construct($id, $text = null, $url = null, $subItems = null)
	{
		$this->id = $id;
		$this->text = isset($text) ? $text : ucfirst($id);
		$this->url = isset($url) ? $url : "page.php?id=$id";
		$this->subItems = $subItems;
	}
	
	function getHtml($currentPageId)
	{
		if ($this->id == $currentPageId)
		{
			$answer = "<b>$this->text</b>";
		}
		else
		{
			$answer = "<a href=\"$this->url\">$this->text</a/";
		}
		return $answer;
	}
}
