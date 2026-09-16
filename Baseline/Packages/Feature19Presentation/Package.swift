// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature19Presentation",
    products: [.library(name: "Feature19Presentation", targets: ["Feature19Presentation"])],
    dependencies: [.package(path: "../Feature19Domain"),
        .package(path: "../Feature19Data")],
    targets: [.target(name: "Feature19Presentation", dependencies: [.product(name: "Feature19Domain", package: "Feature19Domain"), .product(name: "Feature19Data", package: "Feature19Data")])]
)
