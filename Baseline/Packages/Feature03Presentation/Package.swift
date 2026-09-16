// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature03Presentation",
    products: [.library(name: "Feature03Presentation", targets: ["Feature03Presentation"])],
    dependencies: [.package(path: "../Feature03Domain"),
        .package(path: "../Feature03Data")],
    targets: [.target(name: "Feature03Presentation", dependencies: [.product(name: "Feature03Domain", package: "Feature03Domain"), .product(name: "Feature03Data", package: "Feature03Data")])]
)
