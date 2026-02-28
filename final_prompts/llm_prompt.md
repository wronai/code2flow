flowchart TD
    subgraph benchmarks
        benchmarks_benchmark_5139["create_test_project"]
        benchmarks_benchmark_4788["benchmark_original_analyzer"]
        benchmarks_benchmark_1135["benchmark_streaming_analyzer"]
        benchmarks_benchmark_381["benchmark_with_strategies"]
        benchmarks_benchmark_5517["print_comparison"]
        benchmarks_benchmark_performance_main["main"]
    end
    subgraph code2flow
        code2flow_llm_task_generator__strip_bom["_strip_bom"]
        code2flow_llm_task_g_5908["_ensure_list"]
        code2flow_llm_task_generator__deep_get["_deep_get"]
        code2flow_llm_task_g_4827["normalize_llm_task"]
        code2flow_llm_task_g_3176["_parse_bullets"]
        code2flow_llm_task_g_2573["parse_llm_task_text"]
        code2flow_llm_task_generator_load_input["load_input"]
        code2flow_llm_task_generator_dump_yaml["dump_yaml"]
        code2flow_llm_task_g_2733["create_parser"]
        code2flow_llm_task_generator_main["main"]
        code2flow_llm_task_g_6600["start_section"]
        code2flow_mermaid_ge_7362["validate_mermaid_file"]
        code2flow_mermaid_ge_3384["fix_mermaid_file"]
        code2flow_mermaid_ge_66["generate_pngs"]
        code2flow_mermaid_ge_6155["generate_single_png"]
        code2flow_mermaid_ge_6206["generate_with_puppeteer"]
        code2flow_mermaid_ge_1652["strip_label_segments"]
        code2flow_mermaid_ge_4980["sanitize_label_text"]
        code2flow_mermaid_ge_5399["sanitize_node_id"]
        code2flow_mermaid_ge_807["_sanitize_edge_label"]
        code2flow_extractors_5079["__init__"]
        code2flow_extractors_8387["extract"]
        code2flow_extractors_358["new_node"]
        code2flow_extractors_805["connect"]
        code2flow_extractors_3867["visit_FunctionDef"]
        code2flow_extractors_7464["visit_AsyncFunctionDef"]
        code2flow_extractors_1729["visit_If"]
        code2flow_extractors_5807["visit_For"]
        code2flow_extractors_8750["visit_While"]
        code2flow_extractors_3650["visit_Try"]
        code2flow_extractors_6666["visit_Assign"]
        code2flow_extractors_1669["visit_Return"]
        code2flow_extractors_6986["visit_Expr"]
        code2flow_extractors_9017["_qualified_name"]
        code2flow_extractors_7141["_extract_condition"]
        code2flow_extractors_6385["_expr_to_str"]
        code2flow_extractors_3839["_format_except"]
        code2flow_extractors_8975["__init__"]
        code2flow_extractors_5045["extract"]
        code2flow_extractors_9596["new_node"]
        code2flow_extractors_2145["connect"]
        code2flow_extractors_1231["visit_FunctionDef"]
        code2flow_extractors_7454["visit_AsyncFunctionDef"]
        code2flow_extractors_2804["visit_If"]
        code2flow_extractors_424["visit_For"]
        code2flow_extractors_9844["visit_While"]
        code2flow_extractors_2716["visit_Try"]
        code2flow_extractors_6333["visit_Assign"]
        code2flow_extractors_4190["visit_Return"]
        code2flow_extractors_7238["visit_Expr"]
    end
    subgraph setup
        setup_read_readme["read_readme"]
    end
    code2flow_llm_task_g_4827 --> code2flow_llm_task_g_5908
    code2flow_llm_task_g_4827 --> code2flow_llm_task_g_5908
    code2flow_llm_task_g_2573 --> code2flow_llm_task_generator__strip_bom
    code2flow_llm_task_generator_load_input --> code2flow_llm_task_generator__strip_bom
    code2flow_llm_task_generator_load_input --> code2flow_llm_task_g_2573
    code2flow_llm_task_generator_main --> code2flow_llm_task_generator_load_input
    code2flow_llm_task_generator_main --> code2flow_llm_task_g_4827
    code2flow_mermaid_ge_66 --> code2flow_mermaid_ge_7362
    code2flow_mermaid_ge_66 --> code2flow_mermaid_ge_6155
    code2flow_mermaid_ge_66 --> code2flow_mermaid_ge_3384
    code2flow_mermaid_ge_66 --> code2flow_mermaid_ge_7362
    code2flow_mermaid_ge_807 --> code2flow_mermaid_ge_4980
    code2flow_llm_flow_g_4990 --> code2flow_llm_task_generator__strip_bom
    code2flow_llm_flow_g_6418 --> code2flow_llm_flow_g_8912
    code2flow_llm_flow_g_5741 --> code2flow_llm_flow_g_3055
    code2flow_llm_flow_g_5741 --> code2flow_llm_flow_generator_score
    code2flow_llm_flow_g_44 --> code2flow_llm_flow_g_9005
    code2flow_llm_flow_g_44 --> code2flow_llm_flow_g_5430
    code2flow_llm_flow_g_44 --> code2flow_llm_flow_g_6418
    code2flow_llm_flow_g_44 --> code2flow_llm_flow_g_7093
    code2flow_llm_flow_g_44 --> code2flow_llm_flow_g_5741
    code2flow_llm_flow_g_6645 --> code2flow_llm_flow_generator__as_dict
    code2flow_llm_flow_g_6645 --> code2flow_llm_flow_generator__as_list
    code2flow_llm_flow_g_6645 --> code2flow_llm_flow_generator__as_list
    code2flow_llm_flow_g_6645 --> code2flow_llm_flow_generator__as_list
    code2flow_llm_flow_generator_main --> code2flow_llm_flow_g_4990
    code2flow_llm_flow_generator_main --> code2flow_llm_flow_g_44
    code2flow_llm_flow_generator_main --> code2flow_llm_task_generator_dump_yaml
    code2flow_cli_main --> code2flow_llm_task_g_2733
    code2flow_cli_main --> code2flow_cli_generate_llm_context
    code2flow_cli_generate_llm_context --> code2flow_core_analyzer_analyze_project
    benchmarks_benchmark_4788 --> code2flow_core_analyzer_analyze_project
    benchmarks_benchmark_performance_main --> benchmarks_benchmark_5139
    code2flow_exporters__4206 --> code2flow_exporters__1166
    code2flow_exporters__4206 --> code2flow_exporters__1166
    code2flow_exporters__550 --> code2flow_exporters__1166
    code2flow_exporters__550 --> code2flow_exporters__1166
    code2flow_core_analy_869 --> code2flow_core_analyzer_analyze_file
    code2flow_core_analy_8120 --> code2flow_core_analyzer_analyze_file
    code2flow_core_analy_5559 --> code2flow_core_analyzer_analyze_file